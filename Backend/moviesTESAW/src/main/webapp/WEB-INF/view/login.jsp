<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Login</title>

    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
          rel="stylesheet">
</head>
<%
    String error = (String)request.getAttribute("error");
%>
<body class="bg-light">

<div class="container d-flex justify-content-center align-items-center vh-100">

    <div class="card shadow p-4" style="width: 350px;">

        <h3 class="text-center mb-4">Iniciar sesión</h3>

<%
    if (error != null) {
%>
        <div class="alert alert-danger" role="alert">
            <%= error %>
        </div>
<%
    }
%>

        <form action="/autentica" method="post">

            <div class="mb-3">
                <label class="form-label">Usuario</label>
                <input type="text" name="username"
                       class="form-control"
                       placeholder="Introduce tu usuario" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Contraseña</label>
                <input type="password" name="password"
                       class="form-control"
                       placeholder="Introduce tu contraseña" required>
            </div>

            <div class="d-grid">
                <button type="submit" class="btn btn-primary">
                    Entrar
                </button>
            </div>

        </form>

        <hr>

        <div class="text-center small text-muted">
            SessionID: <%= session.getId() %>
        </div>

    </div>

</div>

</body>
</html>