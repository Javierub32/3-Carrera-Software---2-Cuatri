package es.uma.tesaw.demo2026.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class Controlador {

    @GetMapping("/")
    public String doInicio () {
        return "login.html";

    }

    @PostMapping("/login")
    public String doLogin (@RequestParam("user") String usuario,
                           @RequestParam("pwd") String contrasenia,
                           Model model) {
        String respuesta = "";
        if (usuario.equals(contrasenia)) {
            respuesta = "Son iguales!!!";
        } else {
            respuesta = "No son iguales!!!";
        }

        model.addAttribute("respuesta", respuesta);

        return "prueba.jsp";
    }

    @PostMapping("/calculadora")
    public String doCalcular(@RequestParam("op01") Double operador1,
                             @RequestParam("op02") Double operador2,
                             @RequestParam("op03") String operador3,
                             Model model) {
        Double solucion = 0.0;

        switch (operador3) {
            case "+":
                solucion = operador1 + operador2;
                break;
            case "-":
                solucion = operador1 - operador2;
                break;
            case "*":
                solucion = operador1 * operador2;
                break;
            case "/":
                solucion = operador1 / operador2;
                break;
            default:
                solucion = -1.0;
                break;
        }
        model.addAttribute("solucion", solucion);

        return "calculadora.jsp";
    }
}
