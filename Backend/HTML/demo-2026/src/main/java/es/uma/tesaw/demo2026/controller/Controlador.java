package es.uma.tesaw.demo2026.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class Controlador {
    @GetMapping("/inicio")
    public String doInicio() {
        return "prueba.html";
    }

    @PostMapping("/login")
    public String doLogin(@RequestParam("user") String usuario, @RequestParam("pwd") String contrasenia) {
        return "";
    }
}