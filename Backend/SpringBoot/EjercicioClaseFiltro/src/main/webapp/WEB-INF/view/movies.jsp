<%@ page import="es.tesaw.movies.entity.GenreEntity" %>
<%@ page import="java.util.List" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Lista de películas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<%
    List<GenreEntity> generos = (List<GenreEntity>) request.getAttribute("generos");
%>

<h1>Lista de películas</h1>

<form id="form_filtrado">
    <input type="text" name="filtro">
    <%
        for (GenreEntity genero: generos) {
    %>
    <input type="checkbox" name="generos" value="<%= genero.getId() %>"/> <%= genero.getName() %>
    <%
        }
    %>
    <input type="submit" value="Filtrar">
</form>

<div id="tabla">
    <jsp:include page="movies_table.jsp"/>
</div>

<form method="POST" action="/anadir">
    <button type="submit" class="btn btn-primary">Nueva película</button>
</form>

<script>
    const header = document.querySelector("#header");
    const columnasClickables = header.querySelectorAll("th[data-column]");

    let columnaOrden = null;
    let ordenAscendente = true;

    document.getElementById("form_filtrado").addEventListener("submit", (e) => {
        e.preventDefault()
        columnaOrden = null;
        ordenAscendente = true;
        fetchPeliculas()
    });

    document.getElementById("tabla").addEventListener("click", (e) => {
        // No podemos ponerle el listener a los th porque al hacer la petición,
        // se reconstruye la tabla pero los listeners no.
        e.preventDefault()
        const column = e.target.closest("th[data-column]");
        if (column) {
            const ordenarPor = column.dataset.column;
            if (columnaOrden === ordenarPor) {
                ordenAscendente = !ordenAscendente;
            } else {
                    columnaOrden = ordenarPor;
                    ordenAscendente = true;
            }

            fetchPeliculas();
        }
    })


    function fetchPeliculas() {
        const form = document.getElementById("form_filtrado");
        const formData = new FormData(form);

        const params = new URLSearchParams();
        params.append("filtro", formData.get("filtro"));

        const generos = formData.getAll("generos");
        generos.forEach(genero => {
            params.append("generos", genero);
        });

        if (columnaOrden) {
            params.append("ordenarPor", columnaOrden);
            params.append("ascendente", ordenAscendente);
        }

        fetch("/filtrar", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: params.toString()
        })
            .then(response => response.text())
            .then(html => {
                document.getElementById("tabla").innerHTML = html;
            })
            .catch(error => console.error("Error:", error));
    }
</script>

</body>
</html>
