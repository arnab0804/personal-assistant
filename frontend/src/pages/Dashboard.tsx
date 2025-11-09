import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import { Sidebar } from '../components/common/Sidebar';
import { Modal } from '../components/common/Modal';
import { ChatInterface } from '../components/chat/ChatInterface';
import type { Project, Session } from '../types';


export const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();


  const [projects, setProjects] = useState<Project[]>([]);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [selectedSession, setSelectedSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);


  // Modal states
  const [isCreateProjectOpen, setIsCreateProjectOpen] = useState(false);
  const [isCreateSessionOpen, setIsCreateSessionOpen] = useState(false);
  const [isRenameProjectOpen, setIsRenameProjectOpen] = useState(false);
  const [isRenameSessionOpen, setIsRenameSessionOpen] = useState(false);
  const [projectToRename, setProjectToRename] = useState<Project | null>(null);
  const [sessionToRename, setSessionToRename] = useState<Session | null>(null);


  // Form states
  const [newProjectName, setNewProjectName] = useState('');
  const [newSessionTitle, setNewSessionTitle] = useState('');
  const [renameValue, setRenameValue] = useState('');


  useEffect(() => {
    loadData();
  }, []);


  const loadData = async () => {
    try {
      setLoading(true);
      const [projectsData, sessionsData] = await Promise.all([
        apiService.getProjects(),
        apiService.getSessions(),
      ]);
      setProjects(projectsData);
      setSessions(sessionsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };


  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };


  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const newProject = await apiService.createProject({ name: newProjectName });
      setProjects([newProject, ...projects]);
      setNewProjectName('');
      setIsCreateProjectOpen(false);
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };


  const handleCreateSession = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const newSession = await apiService.createSession({
        title: newSessionTitle,
        project_id: selectedProject?.id,
      });
      setSessions([newSession, ...sessions]);
      setNewSessionTitle('');
      setIsCreateSessionOpen(false);
      setSelectedSession(newSession);
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };


  const handleRenameProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectToRename) return;
    try {
      const updated = await apiService.renameProject(projectToRename.id, renameValue);
      setProjects(projects.map(p => (p.id === updated.id ? updated : p)));
      setIsRenameProjectOpen(false);
      setProjectToRename(null);
      setRenameValue('');
    } catch (error) {
      console.error('Error renaming project:', error);
    }
  };


  const handleRenameSession = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sessionToRename) return;
    try {
      const updated = await apiService.renameSession(sessionToRename.id, renameValue);
      setSessions(sessions.map(s => (s.id === updated.id ? updated : s)));
      setIsRenameSessionOpen(false);
      setSessionToRename(null);
      setRenameValue('');
    } catch (error) {
      console.error('Error renaming session:', error);
    }
  };


  const handleDeleteProject = async (project: Project) => {
    if (!confirm(`Delete project "${project.name}"?`)) return;
    try {
      await apiService.deleteProject(project.id);
      setProjects(projects.filter(p => p.id !== project.id));
      if (selectedProject?.id === project.id) {
        setSelectedProject(null);
      }
    } catch (error) {
      console.error('Error deleting project:', error);
    }
  };


  const handleDeleteSession = async (session: Session) => {
    if (!confirm(`Delete session "${session.title}"?`)) return;
    try {
      await apiService.deleteSession(session.id);
      setSessions(sessions.filter(s => s.id !== session.id));
      if (selectedSession?.id === session.id) {
        setSelectedSession(null);
      }
    } catch (error) {
      console.error('Error deleting session:', error);
    }
  };


  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }


  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">rikuduo</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">
                {user?.username}
              </span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>


      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          projects={projects}
          sessions={sessions}
          selectedProject={selectedProject}
          selectedSession={selectedSession}
          onSelectProject={setSelectedProject}
          onSelectSession={setSelectedSession}
          onCreateProject={() => setIsCreateProjectOpen(true)}
          onCreateSession={() => setIsCreateSessionOpen(true)}
          onRenameProject={(project) => {
            setProjectToRename(project);
            setRenameValue(project.name);
            setIsRenameProjectOpen(true);
          }}
          onDeleteProject={handleDeleteProject}
          onRenameSession={(session) => {
            setSessionToRename(session);
            setRenameValue(session.title);
            setIsRenameSessionOpen(true);
          }}
          onDeleteSession={handleDeleteSession}
        />


        <div className="flex-1 flex flex-col bg-gray-50">
          {selectedSession ? (
            <ChatInterface key={selectedSession.id} sessionId={selectedSession.id} />
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  {selectedProject
                    ? selectedProject.name
                    : 'Welcome to rikuduo'}
                </h2>
                <p className="text-gray-600 mb-4">
                  Select a session or create a new one to start chatting
                </p>
                <button
                  onClick={() => setIsCreateSessionOpen(true)}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
                >
                  New Session
                </button>
              </div>
            </div>
          )}
        </div>
      </div>


      {/* Create Project Modal */}
      <Modal
        isOpen={isCreateProjectOpen}
        onClose={() => setIsCreateProjectOpen(false)}
        title="Create New Project"
      >
        <form onSubmit={handleCreateProject}>
          <input
            type="text"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            placeholder="Project name"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
            required
          />
          <div className="mt-4 flex justify-end gap-2">
            <button
              type="button"
              onClick={() => setIsCreateProjectOpen(false)}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
            >
              Create
            </button>
          </div>
        </form>
      </Modal>


      {/* Create Session Modal */}
      <Modal
        isOpen={isCreateSessionOpen}
        onClose={() => setIsCreateSessionOpen(false)}
        title="Create New Session"
      >
        <form onSubmit={handleCreateSession}>
          <input
            type="text"
            value={newSessionTitle}
            onChange={(e) => setNewSessionTitle(e.target.value)}
            placeholder="Session title"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
            required
          />
          <div className="mt-4 flex justify-end gap-2">
            <button
              type="button"
              onClick={() => setIsCreateSessionOpen(false)}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
            >
              Create
            </button>
          </div>
        </form>
      </Modal>


      {/* Rename Project Modal */}
      <Modal
        isOpen={isRenameProjectOpen}
        onClose={() => setIsRenameProjectOpen(false)}
        title="Rename Project"
      >
        <form onSubmit={handleRenameProject}>
          <input
            type="text"
            value={renameValue}
            onChange={(e) => setRenameValue(e.target.value)}
            placeholder="New project name"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
            required
          />
          <div className="mt-4 flex justify-end gap-2">
            <button
              type="button"
              onClick={() => setIsRenameProjectOpen(false)}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
            >
              Rename
            </button>
          </div>
        </form>
      </Modal>


      {/* Rename Session Modal */}
      <Modal
        isOpen={isRenameSessionOpen}
        onClose={() => setIsRenameSessionOpen(false)}
        title="Rename Session"
      >
        <form onSubmit={handleRenameSession}>
          <input
            type="text"
            value={renameValue}
            onChange={(e) => setRenameValue(e.target.value)}
            placeholder="New session title"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
            required
          />
          <div className="mt-4 flex justify-end gap-2">
            <button
              type="button"
              onClick={() => setIsRenameSessionOpen(false)}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
            >
              Rename
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};