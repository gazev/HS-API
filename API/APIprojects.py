from flask import Blueprint, request, jsonify, session
# Importing the methods for the projects
from API import handlers
from Tags import Tags

# AVISO À NAVEGAÇÃO
# As routs aqui presentes apresentam cabaçalhos que não fazem muito sentido
# no contexto da chamada à base de dados. Por isso ainda existe muita coisa a ser
# feita, nomeadamente:
# - Ajustar os cabaçalhos das rotas
# - DEFINIR QUAL O CORPO DOS REQUESTS/POSTS

############# Projects #############
def createProjectBlueprint(handlers: handlers.Handlers, login_required, tags: Tags):
    project_bp = Blueprint('projects', __name__)

    projectHandler = handlers.projectHandler
    memberProjectHandler = handlers.memberProjectHandler

    @project_bp.route('/projects', methods=['GET'])
    @login_required
    def get_projects():
        projects = projectHandler.listProjects()
        return jsonify(projects)
    
    @project_bp.route('/projects', methods=['POST'])
    @login_required
    def create_project():
        # Does the user have permition to create a project
        user_tags = session['tags'].split(',')
        if not tags.can(user_tags, 'create_project'):
            return jsonify({'message': 'You do not have permission to create a project'}), 403

        data = request.json
        projectHandler.createProject(data['name'], data['description'], data['tags'], data['members'])
        return jsonify({'message': 'Project created successfully!'})
    
    @project_bp.route('/projects/<int:project_id>', methods=['GET'])
    @login_required
    def get_project(project_id):
        project_data = projectHandler.getProject(project_id)
        return jsonify(project_data)
    
    @project_bp.route('/projects/<int:project_id>', methods=['PUT'])
    @login_required
    def update_project(project_id):
        # Does the user have permition to update a project
        user_tags = session['tags'].split(',')
        if not tags.can(user_tags, 'edit_project'):
            return jsonify({'message': 'You do not have permission to edit a project'}), 403

        data = request.json
        projectHandler.updateProject(project_id, data['name'], data['description'], data['tags'], data['members'])
        return jsonify({'message': 'Project updated successfully!'})
    
    @project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
    @login_required
    def delete_project(project_id):
        # Does the user have permition to delete a project
        user_tags = session['tags'].split(',')
        if not tags.can(user_tags, 'delete_project'):
            return jsonify({'message': 'You do not have permission to delete a project'}), 403

        projectHandler.deleteProject(project_id)
        return jsonify({'message': 'Project deleted successfully!'})
    
    @project_bp.route('/projects/<int:project_id>/members', methods=['GET'])
    @login_required
    def get_project_members(project_id):
        members = memberProjectHandler.listMembers(project_id)
        return jsonify(members)
    
    return project_bp