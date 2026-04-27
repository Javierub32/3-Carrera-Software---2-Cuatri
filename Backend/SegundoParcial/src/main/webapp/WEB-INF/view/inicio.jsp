<%@ page import="es.taw.movies.entity.ProductionCompanies" %>
<%@ page import="java.util.List" %>
<%@ page import="es.taw.movies.entity.Movies" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<%
    List<ProductionCompanies> productionCompanies = (List<ProductionCompanies>) request.getAttribute("productionCompanies");
    List<Movies> movies = (List<Movies>) request.getAttribute("movies");

%>
<h1>Pestaña Principal</h1>
<div style="display: flex; flex-direction: row; justify-content: space-around; ">
<div>
    <h2>Productoras</h2>
    <div>
        <% for(ProductionCompanies p : productionCompanies) {%>
        <p>
            <%=p.getName()%> <input type="checkbox" name="productoras" value="<%=p.getId()%>">
        </p>
        <%}%>
    </div>
</div>
<div>
    <h2>Peliculas</h2>
    <div>
        <% for(ProductionCompanies p : productionCompanies) {%>
            <% for(Movies m : p.getMoviesList()) {%>
            <p>
                <a href="#"><%=m.getTitle()%></a>
            </p>
            <%}%>
        <%}%>


    </div>
</div>
</div>
</body>
</html>
