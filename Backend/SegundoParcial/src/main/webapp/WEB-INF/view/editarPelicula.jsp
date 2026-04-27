<%@ page import="java.util.List" %>
<%@ page import="es.taw.movies.entity.*" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<%
    Movies movie = (Movies) request.getAttribute("movie");
    List<SpokenLanguages> languages = (List<SpokenLanguages>) request.getAttribute("languages");
    List<SpokenLanguages> movieLanguages = (List<SpokenLanguages>) request.getAttribute("movieLanguages");
    List<MovieCast> peopleCast = (List<MovieCast>) request.getAttribute("peopleCast");
    List<MovieCrew> peopleCrew = (List<MovieCrew>) request.getAttribute("peopleCrew");

%>
<h1>Ficha de pelicula</h1>
<div style="display: flex; flex-direction: row">
<form action="/guardarPelicula" method="post">
    <input type="hidden" name="id" value="<%=movie.getId()%>">
    <p>
        <label for="1">Titulo: </label>
        <input type="text" id="1" value="<%=movie.getTitle()%>" name="title">
    </p>

    <p>
        <label for="2">Fecha Publicacion: </label>
        <input type="date" id="2" value="<%=movie.getReleaseDate()%>" name="fecha">
    </p>

    <p>
        <label for="3">Presupuesto: </label>
        <input type="text" id="3" value="<%=movie.getBudget()%>" name="presupuesto">
    </p>
    <p>
        <label for="">Idiomas disponibles: </label>
        <% for(SpokenLanguages i: languages) {%>
            <input type="checkbox" name="languages" value="<%=i.getIso6391()%>" <%=movieLanguages != null && movieLanguages.contains(i) ? "checked" : ""%>> <%=i.getName()%>
        <%}%>
    </p>
    <p>
        <label for="4">Sinopsis: </label>
        <input type="text" id="4" value="<%=movie.getOverview()%>" name="sinopsis">
    </p>
    <button type="submit">Guardar</button>
</form>
    <div style="border: 1px solid black; margin: 10px; padding: 7px">
        <% for(MovieCast mc: peopleCast) {%>
            <p>
                <%=mc.getCharacterName()%> - <%=mc.getPersonId().getName()%>
            </p>

        <%}%>

        <% for(MovieCrew mc: peopleCrew) {%>
            <p>
                <%=mc.getJob()%> - <%=mc.getPersonId().getName()%>
            </p>
        <%}%>
        <a href="/editarPelicula?id=<%=movie.getId()%>&filtro=reparto">Reparto</a>
        <a href="/editarPelicula?id=<%=movie.getId()%>&filtro=trabajadores">Trabajadores</a>
    </div>
</div>
</body>
</html>
