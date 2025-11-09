import { useState } from 'react';
import { Plus, Folder, MessageSquare, Pencil, Trash2 } from 'lucide-react';
import type { Project, Session } from '../../types';


interface SidebarProps {
  projects: Project[];
  sessions: Session[];
  selectedProject: Project | null;
  selectedSession: Session | null;
  onSelectProject: (project: Project | null) => void;
  onSelectSession: (session: Session) => void;
  onCreateProject: () => void;
  onCreateSession: () => void;
  onRenameProject: (project: Project) => void;
  onDeleteProject: (project: Project) => void;
  onRenameSession: (session: Session) => void;
  onDeleteSession: (session: Session) => void;
}


export const Sidebar = ({
  projects,
  sessions,
  selectedProject,
  selectedSession,
  onSelectProject,
  onSelectSession,
  onCreateProject,
  onCreateSession,
  onRenameProject,
  onDeleteProject,
  onRenameSession,
  onDeleteSession,
}: SidebarProps) => {
  const [expandedProjects, setExpandedProjects] = useState<Set<string>>(new Set());


  const toggleProject = (projectId: string) => {
    const newExpanded = new Set(expandedProjects);
    if (newExpanded.has(projectId)) {
      newExpanded.delete(projectId);
    } else {
      newExpanded.add(projectId);
    }
    setExpandedProjects(newExpanded);
  };


  const getProjectSessions = (projectId: string) => {
    return sessions.filter(s => s.project_id === projectId);
  };


  const getUnassignedSessions = () => {
    return sessions.filter(s => !s.project_id);
  };


  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col h-full">
      {/* Projects Section */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-gray-700">Projects</h2>
          <button
            onClick={onCreateProject}
            className="p-1 hover:bg-gray-100 rounded"
            title="New Project"
          >
            <Plus className="w-4 h-4 text-gray-600" />
          </button>
        </div>


        <div className="space-y-1">
          {/* All Sessions */}
          <button
            onClick={() => onSelectProject(null)}
            className={`w-full flex items-center gap-2 px-2 py-1.5 rounded text-sm ${
              !selectedProject
                ? 'bg-blue-50 text-blue-700'
                : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            <span>All Sessions</span>
          </button>


          {/* Project List */}
          {projects.map((project) => (
            <div key={project.id}>
              <div
                className={`flex items-center gap-2 px-2 py-1.5 rounded text-sm cursor-pointer ${
                  selectedProject?.id === project.id
                    ? 'bg-blue-50 text-blue-700'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <button
                  onClick={() => {
                    onSelectProject(project);
                    toggleProject(project.id);
                  }}
                  className="flex items-center gap-2 flex-1"
                >
                  <Folder className="w-4 h-4" />
                  <span className="truncate">{project.name}</span>
                </button>
                <div className="flex items-center gap-1">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onRenameProject(project);
                    }}
                    className="p-1 hover:bg-gray-200 rounded"
                    title="Rename"
                  >
                    <Pencil className="w-3 h-3" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteProject(project);
                    }}
                    className="p-1 hover:bg-red-100 rounded"
                    title="Delete"
                  >
                    <Trash2 className="w-3 h-3 text-red-600" />
                  </button>
                </div>
              </div>


              {/* Project Sessions */}
              {expandedProjects.has(project.id) && (
                <div className="ml-6 mt-1 space-y-1">
                  {getProjectSessions(project.id).map((session) => (
                    <div
                      key={session.id}
                      className={`flex items-center gap-2 px-2 py-1 rounded text-xs cursor-pointer ${
                        selectedSession?.id === session.id
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      <button
                        onClick={() => onSelectSession(session)}
                        className="flex-1 text-left truncate"
                      >
                        {session.title}
                      </button>
                      <div className="flex items-center gap-1">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onRenameSession(session);
                          }}
                          className="p-1 hover:bg-gray-200 rounded"
                          title="Rename"
                        >
                          <Pencil className="w-2.5 h-2.5" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDeleteSession(session);
                          }}
                          className="p-1 hover:bg-red-100 rounded"
                          title="Delete"
                        >
                          <Trash2 className="w-2.5 h-2.5 text-red-600" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>


      {/* Sessions Section */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-gray-700">Recent Sessions</h2>
          <button
            onClick={onCreateSession}
            className="p-1 hover:bg-gray-100 rounded"
            title="New Session"
          >
            <Plus className="w-4 h-4 text-gray-600" />
          </button>
        </div>


        <div className="space-y-1">
          {getUnassignedSessions().map((session) => (
            <div
              key={session.id}
              className={`flex items-center gap-2 px-2 py-1.5 rounded text-sm cursor-pointer ${
                selectedSession?.id === session.id
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-50'
              }`}
            >
              <button
                onClick={() => onSelectSession(session)}
                className="flex-1 text-left truncate"
              >
                {session.title}
              </button>
              <div className="flex items-center gap-1">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onRenameSession(session);
                  }}
                  className="p-1 hover:bg-gray-200 rounded"
                  title="Rename"
                >
                  <Pencil className="w-3 h-3" />
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteSession(session);
                  }}
                  className="p-1 hover:bg-red-100 rounded"
                  title="Delete"
                >
                  <Trash2 className="w-3 h-3 text-red-600" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};