// Cliente HTTP tipado para la API de Kitchi Studio (Django REST Framework).
// Token expedido por /api/auth/login/ en el flujo de registro o login.
import type { ApiErrorEnvelope, CatRecord, Paginated, ProfileRecord, PublicationRecord, UserRecord } from './types';

const SDK_OUT_OF_ORDER = 'SDK_OUT_OF_ORDER';

export class ApiError extends Error {
  code: string;
  status: number | null;
  details: unknown;
  constructor(code: string, message: string, status: number | null = null, details: unknown = {}) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.status = status;
    this.details = details;
  }
  userMessage(): string {
    const d = this.details as Record<string, unknown> | null;
    if (!d || typeof d !== 'object') return this.message;
    for (const key of ['campos', 'campo']) {
      const value = d[key];
      if (!value) continue;
      const parts: string[] = [];
      if (Array.isArray(value)) parts.push(...value.map((v) => String(v)));
      else if (typeof value === 'object') for (const v of Object.values(value)) parts.push(String(v));
      else parts.push(String(value));
      if (parts.length) return parts.join(' ');
    }
    if (typeof d['detail'] === 'string') return d['detail'];
    return this.message;
  }
}

function decode(raw: string): unknown {
  if (!raw) return {};
  try { return JSON.parse(raw); } catch { return { raw }; }
}

function resolveBaseUrl(): string {
  const envUrl = (import.meta.env.VITE_API_URL as string | undefined) ?? '';
  if (envUrl) return envUrl.replace(/\/+$/, '');
  // Fallback al host del API local (backend Django)
  return 'http://127.0.0.1:8000';
}

export interface ClientOptions {
  baseUrl?: string;
}

class ApiClient {
  baseUrl: string;
  token: string | null = null;

  constructor(opts: ClientOptions = {}) {
    this.baseUrl = opts.baseUrl ?? resolveBaseUrl();
  }

  setToken(token: string | null): void {
    this.token = token?.trim() || null;
  }

  get mode(): 'http' | 'local' {
    return this.baseUrl ? 'http' : 'local';
  }

  private async request<T = unknown>(method: string, path: string, data?: unknown): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const headers: Record<string, string> = { Accept: 'application/json' };
    if (data !== undefined) {
      headers['Content-Type'] = 'application/json; charset=utf-8';
    }
    if (this.token) headers['Authorization'] = `Token ${this.token}`;
    let res: Response;
    try {
      res = await fetch(url, {
        method,
        headers,
        body: data === undefined ? undefined : JSON.stringify(data),
      });
    } catch {
      throw new ApiError('API_UNREACHABLE', 'No se pudo conectar con la API.', null);
    }
    const text = await res.text();
    const payload = decode(text) as Record<string, unknown>;
    if (!res.ok) {
      const envelope = payload as unknown as ApiErrorEnvelope;
      const e = envelope?.error ?? {};
      throw new ApiError(e.code ?? `HTTP_${res.status}`, e.message ?? `Error HTTP ${res.status}`, res.status, e.details ?? {});
    }
    return payload as T;
  }

  async health(): Promise<{ status: string }> {
    if (this.mode === 'local') return { status: 'local-mode' };
    return this.request<{ status: string }>('GET', '/api/health/');
  }

  async getCatalog(): Promise<unknown> {
    return this.request('GET', '/api/catalog/');
  }

  async getPoses(): Promise<Array<{ code: string; name: string }>> {
    const payload = await this.request<{ results?: Array<{ code: string; name: string }> } | Array<{ code: string; name: string }>>('GET', '/api/poses/');
    if (Array.isArray(payload)) return payload;
    return payload?.results ?? [];
  }

  async register(username: string, email: string, password: string): Promise<{ token: string; user: UserRecord }> {
    return this.request('POST', '/api/auth/register/', { username, email, password });
  }

  async login(username: string, password: string): Promise<{ token: string; user: UserRecord }> {
    return this.request('POST', '/api/auth/login/', { username, password });
  }

  async logout(): Promise<void> {
    if (this.mode !== 'http') return;
    try { await this.request('POST', '/api/auth/logout/'); } catch { /* token puede ya no existir */ }
    this.token = null;
  }

  async me(): Promise<UserRecord> {
    return this.request<UserRecord>('GET', '/api/auth/me/');
  }

  async listCats(): Promise<CatRecord[]> {
    const data = await this.request<{ results?: CatRecord[] } | CatRecord[]>('GET', '/api/cats/');
    if (Array.isArray(data)) return data;
    return data?.results ?? [];
  }

  async createCat(name: string, configuration: unknown): Promise<CatRecord> {
    return this.request<CatRecord>('POST', '/api/cats/', { name, configuration });
  }

  async updateCat(id: number | string, body: Partial<CatRecord>): Promise<CatRecord> {
    return this.request<CatRecord>('PATCH', `/api/cats/${id}/`, body);
  }

  async deleteCat(id: number | string): Promise<void> {
    await this.request('DELETE', `/api/cats/${id}/`);
  }

  async getPublications(opts: { page?: number; page_size?: number; q?: string; user?: string } = {}): Promise<Paginated<PublicationRecord>> {
    const params = new URLSearchParams();
    if (opts.page) params.set('page', String(opts.page));
    if (opts.page_size) params.set('page_size', String(opts.page_size));
    if (opts.q) params.set('q', opts.q);
    if (opts.user) params.set('user', opts.user);
    const qs = params.toString();
    const data = await this.request<Paginated<PublicationRecord>>('GET', `/api/publications/${qs ? `?${qs}` : ''}`);
    return data;
  }

  async publishCat(id: number | string, title: string, description: string, visibility: 'public' | 'private'): Promise<PublicationRecord> {
    return this.request<PublicationRecord>('POST', '/api/publications/', { cat_id: id, title, description, visibility });
  }

  async getPublication(id: number): Promise<PublicationRecord> {
    return this.request<PublicationRecord>('GET', `/api/publications/${id}/`);
  }

  async getPublicProfile(username: string): Promise<ProfileRecord> {
    return this.request<ProfileRecord>('GET', `/api/profiles/${encodeURIComponent(username)}/`);
  }
}

export const api = new ApiClient();
export { SDK_OUT_OF_ORDER };

export type { PublicationRecord, ProfileRecord, CatRecord, Paginated, UserRecord };
