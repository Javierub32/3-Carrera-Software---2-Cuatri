<%--
  Created by IntelliJ IDEA.
  User: javie
  Date: 02/03/2026
  Time: 11:17
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<form method="post" action="/calculadora">
    Operador 1: <input type="text" id="operador1" name="op01" value="${solucion}" />
    Operador 2: <input type="text" id="operador2" name="op02" />
    Operador:
    <input type="radio" name="op03" value="+" /> +
    <input type="radio" name="op03" value="-" /> -
    <input type="radio" name="op03" value="*" /> *
    <input type="radio" name="op03" value="/" /> /
    <button>Enviar</button>
</form>
<h1>El resultado es ${solucion}</h1>


</body>
</html>
