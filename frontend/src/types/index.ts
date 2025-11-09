export interface User {
  id: string;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}


export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}


export interface LoginCredentials {
  identifier: string;
  password: string;
}


export interface SignupData {
  email: string;
  username: string;
  password: string;
}


export interface Project {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  tags: string[];
  default_llm_model: string | null;
  default_system_prompt: string | null;
  settings: Record<string, any>;
  created_at: string;
  updated_at: string;
}


export interface ProjectCreate {
  name: string;
  description?: string;
  tags?: string[];
  default_llm_model?: string;
  default_system_prompt?: string;
}


export interface Session {
  id: string;
  user_id: string;
  project_id: string | null;
  title: string;
  mode: 'chat' | 'code' | 'research' | 'translation' | 'council' | 'agent';
  llm_model: string | null;
  system_prompt: string | null;
  settings: Record<string, any>;
  context_summary: string | null;
  created_at: string;
  updated_at: string;
}


export interface SessionCreate {
  title: string;
  mode?: 'chat' | 'code' | 'research' | 'translation' | 'council' | 'agent';
  project_id?: string;
  llm_model?: string;
  system_prompt?: string;
}


export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  sequence: number;
  llm_model: string | null;
  prompt_tokens: number | null;
  completion_tokens: number | null;
  total_tokens: number | null;
  meta: Record<string, any>;
  agent_name: string | null;
  is_summary: boolean;
  created_at: string;
}