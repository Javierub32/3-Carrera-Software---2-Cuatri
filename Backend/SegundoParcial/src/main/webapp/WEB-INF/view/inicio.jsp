<%@ page import="es.taw.movies.entity.ProductionCompanies" %>
<%@ page import="java.util.List" %>
<%@ page import="es.taw.movies.entity.Movies" %>
<%@ page import="es.taw.movies.entity.SpokenLanguages" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<%
    List<ProductionCompanies> productionCompanies = (List<ProductionCompanies>) request.getAttribute("productionCompanies");
    List<Movies> movies = (List<Movies>) request.getAttribute("movies");
    List<Integer> idsProductoras = (List<Integer>) request.getAttribute("idsProductoras");

%>
<h1>Pestaña Principal</h1>
<div style="display: flex; flex-direction: row; justify-content: space-around; ">
<div>
    <h2>Productoras</h2>
    <div>
        <form action="/filtrarPeliculas" method="post">
            <% for(ProductionCompanies p : productionCompanies) {%>
                <p>

                    <%=p.getName()%> <input type="checkbox" name="productoras" value="<%=p.getId()%>"
                    <%=idsProductoras != null && idsProductoras.contains(p.getId()) ? "checked" : "" %>>


                </p>
            <%}%>
            <button type="submit">Filtrar</button>
        </form>

    </div>
</div>
<div>
    <h2>Peliculas</h2>
    <div>
        <% for(Movies m : movies) {%>
            <p>
                <a href="/editarPelicula?id=<%=m.getId()%>" ><%=m.getTitle()%></a> (
                <% for(SpokenLanguages l : m.getSpokenLanguagesList()) {%>
                    <%=l.getName()%>
                <%}%>
                )
            </p>

        <%}%>


    </div>
</div>
</div>
</body>
</html>
