import axios, { type AxiosInstance, type AxiosError } from 'axios';


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';


class ApiService {
  private api: AxiosInstance;


  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });


    // Add request interceptor to include auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );


    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }


  // Auth endpoints
  async signup(data: { email: string; username: string; password: string }) {
    const response = await this.api.post('/auth/signup', data);
    return response.data;
  }


  async login(data: { identifier: string; password: string }) {
    const response = await this.api.post('/auth/login', data);
    return response.data;
  }


  async getCurrentUser() {
    const response = await this.api.get('/auth/me');
    return response.data;
  }


  async logout() {
    const response = await this.api.post('/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    return response.data;
  }


  // Project endpoints
  async getProjects() {
    const response = await this.api.get('/projects/');
    return response.data;
  }


  async createProject(data: any) {
    const response = await this.api.post('/projects/', data);
    return response.data;
  }


  async getProject(projectId: string) {
    const response = await this.api.get(`/projects/${projectId}`);
    return response.data;
  }


  async updateProject(projectId: string, data: any) {
    const response = await this.api.put(`/projects/${projectId}`, data);
    return response.data;
  }


  async renameProject(projectId: string, name: string) {
    const response = await this.api.patch(`/projects/${projectId}/rename`, { name });
    return response.data;
  }


  async deleteProject(projectId: string) {
    const response = await this.api.delete(`/projects/${projectId}`);
    return response.data;
  }


  // Session endpoints
  async getSessions(projectId?: string) {
    const params = projectId ? { project_id: projectId } : {};
    const response = await this.api.get('/chat/sessions', { params });
    return response.data;
  }


  async createSession(data: any) {
    const response = await this.api.post('/chat/sessions', data);
    return response.data;
  }


  async getSession(sessionId: string) {
    const response = await this.api.get(`/chat/sessions/${sessionId}`);
    return response.data;
  }


  async updateSession(sessionId: string, data: any) {
    const response = await this.api.put(`/chat/sessions/${sessionId}`, data);
    return response.data;
  }


  async renameSession(sessionId: string, title: string) {
    const response = await this.api.patch(`/chat/sessions/${sessionId}/rename`, { title });
    return response.data;
  }


  async deleteSession(sessionId: string) {
    const response = await this.api.delete(`/chat/sessions/${sessionId}`);
    return response.data;
  }


  async getSessionMessages(sessionId: string) {
    const response = await this.api.get(`/chat/sessions/${sessionId}/messages`);
    return response.data;
  }


  // Generic methods
  async get(url: string, config = {}) {
    const response = await this.api.get(url, config);
    return response.data;
  }


  async post(url: string, data = {}, config = {}) {
    const response = await this.api.post(url, data, config);
    return response.data;
  }


  async put(url: string, data = {}, config = {}) {
    const response = await this.api.put(url, data, config);
    return response.data;
  }


  async delete(url: string, config = {}) {
    const response = await this.api.delete(url, config);
    return response.data;
  }
}


export const apiService = new ApiService();