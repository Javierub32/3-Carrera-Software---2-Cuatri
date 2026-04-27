package es.taw.movies.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MoviesController {

    @GetMapping("/")
    public String doInit() {
        return "inicio";
    }
}
