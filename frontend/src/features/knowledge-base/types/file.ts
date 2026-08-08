export type FileStatus =
  | "uploading"
  | "pending"
  | "indexing"
  | "ready"
  | "failed"
  | "deleting";

export interface IndexedFile {
  id: string;
  name: string;
  size: number;
  mimeType: string;
  status: FileStatus;
  createdAt: string;
  updatedAt: string;
  indexedAt?: string | null;
  chunkCount?: number;
  errorMessage?: string | null;
}