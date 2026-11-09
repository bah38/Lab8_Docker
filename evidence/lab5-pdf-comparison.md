# Comparison with the Lab 5 PDF

Reference: user-supplied `lab5_repo+screenshots (2).pdf`, five pages.
The PDF names https://github.com/bah38/Lab5_Postman_API, which is the repository used by the Lab 8 port-5000 image.

| PDF page | Method and route | Result shown | Lab 8 comparison |
| --- | --- | --- | --- |
| 1 | GET /api/users | 200, empty JSON list | Matches the original empty database and container verification |
| 2 | POST /api/users/add | 200, created user object | Same route and fields: user_id, name, email, phone, address, country |
| 3 | GET /api/users/1 | 200, user object | Same route with a variable user ID |
| 4 | PUT /api/users/update | 200, updated user object | Same route and fields |
| 5 | DELETE /api/users/delete/1 | 200, User deleted successfully | Same route and success message |

The PDF contains Postman example views from the earlier Lab 5 submission. These are historical reference images; Lab 8 runtime evidence remains the actual Docker and terminal screenshots in this package.

No application changes were needed. The Lab 5 image keeps the original routes, with Flask bound to 0.0.0.0:5000 for Docker networking. The port-3000 GET /get_users endpoint is the additional Lab 8 requirement. Temporary test records were removed after container verification.
