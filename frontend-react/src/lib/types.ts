export type Visibility = 'public' | 'private';

export interface CatRecord {
  id: number | string;
  name: string;
  configuration: Record<string, unknown>;
  created_at?: string;
  updated_at?: string;
}

export interface PublicationRecord {
  id: number;
  title: string;
  description: string;
  visibility: Visibility;
  author: string;
  cat: CatRecord | null;
  created_at: string;
  updated_at: string;
}

export interface UserRecord {
  id: number;
  username: string;
  email?: string;
  role?: 'member' | 'admin';
  premium?: boolean;
  date_joined?: string;
}

export interface ProfileRecord {
  username: string;
  joined_at?: string;
  publication_count: number;
  cats: CatRecord[];
  publications: PublicationRecord[];
}

export interface Paginated<T> {
  count: number;
  next?: string | null;
  previous?: string | null;
  results: T[];
}

export interface ApiErrorEnvelope {
  error: { code: string; message: string; details?: unknown };
}
