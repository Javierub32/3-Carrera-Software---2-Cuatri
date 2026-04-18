<%@ page import="es.tesaw.movies.entity.MovieEntity" %>
<%@ page import="es.tesaw.movies.entity.SpokenLanguageEntity" %>
<%@ page import="java.util.List" %>
<%@ page import="es.tesaw.movies.entity.GenreEntity" %><%--
  Created by IntelliJ IDEA.
  User: guzman
  Date: 18/3/26
  Time: 12:09
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>(peli.getId()!=null?"Editar":"Crear") %> película</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
          rel="stylesheet">
</head>
<%
    MovieEntity peli = (MovieEntity) request.getAttribute("pelicula");
    List<SpokenLanguageEntity> idiomas = (List<SpokenLanguageEntity>) request.getAttribute("idiomas");
    List<GenreEntity> generos = (List<GenreEntity>) request.getAttribute("generos");
%>
<body>
<div class="container mt-5">
    <h2 class="mb-4"><%= (peli.getId()!=null?"Editar":"Crear") %> Película</h2>

<form action="/guardar" method="post">
    <%
        if (peli.getId() != null) {
    %>
    <input type="hidden" name="id" value="<%= peli.getId() %>">
    <%
        }
    %>
    <div class="mb-3">
        <label class="form-label">Título:</label>
        <input class="form-control" type="text" size="100" maxlength="100" name="titulo" value="<%= (peli.getId()!=null?peli.getTitle():"") %>"/><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Título original:</label>
            <input class="form-control" type="text" name="titulo_orig" value="<%= (peli.getId()!=null?peli.getOriginalTitle():"") %>"/><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Idioma:</label>
        <select name="idioma" class="form-control">
            <%
                for (SpokenLanguageEntity idioma: idiomas) {
                    String selected = "";
                    if (peli.getId()!= null && idioma.getId() == peli.getOriginalLanguage().getId())
                        selected = "selected";
            %>
                    <option value="<%= idioma.getId() %>" <%= selected %> ><%= idioma.getName()%></option>
            <%
                }
            %>
        </select>
        <br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Géneros: </label>
        <%
            for (GenreEntity genero: generos) {
                String checked = "";
                if (peli.getId()!= null && peli.getGenres().contains(genero))
                    checked = "checked";
        %>

        <input type="checkbox" <%= checked %> name="generos" value="<%= genero.getId() %>"><%= genero.getName() %>

        <%
            }
        %>

    </div>
    <div class="mb-3">
        <label class="form-label">Sinopsis: </label>
        <textarea class="form-control" rows="10" cols="50" name="sinopsis"><%= (peli.getId()!=null?peli.getOverview():"") %></textarea><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Fecha de estreno: </label>
        <input class="form-control" type="date" name="fecha" value="<%= (peli.getId()!=null?peli.getReleaseDate():"") %>"/><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Duración: </label>
        <input class="form-control" type="text" name="runtime" value="<%= (peli.getId()!=null?peli.getRuntime():"") %>"/><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Presupuesto: </label>
        <input class="form-control" type="number" name="budget" value="<%= (peli.getId()!=null?peli.getBudget():"") %>" /><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Ingresos: </label>
        <input class="form-control" type="number" name="revenue" value="<%= (peli.getId()!=null?peli.getRevenue():"") %>" /><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Estado: </label>
        <input class="form-control" type="number" name="status" value="<%=(peli.getId()!=null?peli.getStatus():"") %>" /><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Tagline: </label>
        <input class="form-control" type="text" size="100" maxlength="100" name="tagline" value="<%= (peli.getId()!=null?peli.getTagline():"") %>"/><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Popularidad: </label>
        <input class="form-control" type="number" name="popularity" value="<%= (peli.getId()!=null?peli.getPopularity():"") %>" /><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Calificación promedio: </label>
        <input class="form-control" type="number" name="voteAverage" value="<%= (peli.getId()!=null?peli.getVoteAverage():"") %>" /><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Número de votos: </label>
        <input class="form-control" type="number" name="voteCount" value="<%= (peli.getId()!=null?peli.getVoteCount():"") %>" /><br/>
    </div>
    <div class="mb-3">
        <label class="form-label">Sitio web: </label>
        <input class="form-control" type="text" size="100" maxlength="100" name="homepage" value="<%= (peli.getId()!=null?peli.getHomepage():"") %>"/><br/>
    </div>

    <button type="submit">Guardar</button>
</form>
</div>
</body>
</html>
