export interface HealthData {
  status: string;
}

export interface StandardApiResponse<T = any> {
  success: boolean;
  data: T | null;
  message: string;
  errors?: Record<string, any>;
}

export type ConnectionState = 'loading' | 'success' | 'failure';

export interface TestResultItem {
  id: string;
  category: 'Backend' | 'Flutter' | 'Security';
  name: string;
  status: 'passed' | 'failed';
  detail: string;
}

export interface ProjectFileItem {
  path: string;
  name: string;
  category: 'backend' | 'mobile' | 'infrastructure' | 'docs' | 'root';
  description: string;
  content: string;
}
