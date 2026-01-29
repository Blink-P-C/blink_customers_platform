export enum UserRole {
  ADMIN = 'admin',
  CLIENT = 'client',
}

export enum ProjectStatus {
  ACTIVE = 'active',
  COMPLETED = 'completed',
  ON_HOLD = 'on_hold',
  CANCELLED = 'cancelled',
}

export enum BookingStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  CANCELLED = 'cancelled',
  COMPLETED = 'completed',
}

export enum RequestType {
  IMPROVEMENT = 'improvement',
  REVISION = 'revision',
  BUG = 'bug',
  QUESTION = 'question',
}

export enum RequestStatus {
  OPEN = 'open',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

export interface User {
  id: number
  email: string
  full_name: string
  role: UserRole
  is_active: boolean
  created_at: string
  updated_at?: string
}

export interface Project {
  id: number
  name: string
  description?: string
  status: ProjectStatus
  start_date?: string
  end_date?: string
  created_at: string
  updated_at?: string
}

export interface Recording {
  id: number
  project_id: number
  title: string
  description?: string
  sharepoint_file_id?: string
  sharepoint_url?: string
  duration_seconds?: number
  file_size_bytes?: number
  created_at: string
  updated_at?: string
}

export interface Booking {
  id: number
  user_id: number
  slot_id?: number
  title: string
  description?: string
  start_time: string
  end_time: string
  status: BookingStatus
  google_event_id?: string
  meeting_link?: string
  created_at: string
  updated_at?: string
}

export interface AvailabilitySlot {
  id: number
  start_time: string
  end_time: string
  is_available: boolean
  created_at: string
}

export interface File {
  id: number
  project_id: number
  name: string
  description?: string
  sharepoint_file_id?: string
  sharepoint_url?: string
  file_size_bytes?: number
  mime_type?: string
  created_at: string
  updated_at?: string
}

export interface RequestMessage {
  id: number
  request_id: number
  user_id: number
  message: string
  created_at: string
}

export interface Request {
  id: number
  user_id: number
  project_id: number
  title: string
  description: string
  type: RequestType
  status: RequestStatus
  created_at: string
  updated_at?: string
  messages: RequestMessage[]
}
