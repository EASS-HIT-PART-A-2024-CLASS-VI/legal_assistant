### Project Application Structure (Backend)
| Folder Name | Purpose                                                                                |
|-------------|----------------------------------------------------------------------------------------|
| api         | Data Access Layer - Contains API routes with their models, controllers, and services   |
| development | Resources for local development and deployment configurations                          |
| engine      | Core business logic implementing the RAG (Retrieval Augmented Generation) graph system |
| utils       | Common utility functions, helpers, and shared components used across the application   |
| integration       | Testing cross module functionality and integration with external systems.   |
| unit_tests       | Testing functions mainly. *MUST* not communicate with any external system   |



### Project Application Structure (Frontend)
| Folder Name  | Purpose                                                                                |
|--------------|----------------------------------------------------------------------------------------|
| componenttts |  Reusable UI components and building blocks of the application                         |
| pages        | Page-level components and routing logic for different application views |
| utils        | Common utility functions, helpers, and shared components used across the application   |
| integration  | Testing cross module functionality and integration with external systems.   |
| unit_tests   | Testing functions mainly. *MUST* not communicate with any external system   |                                                                               |

