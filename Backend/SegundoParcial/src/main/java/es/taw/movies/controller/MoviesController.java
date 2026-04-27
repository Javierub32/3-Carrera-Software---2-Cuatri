package es.taw.movies.controller;

import es.taw.movies.entity.ProductionCompanies;
import es.taw.movies.repository.ProductionCompaniesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class MoviesController {
    @Autowired
    private ProductionCompaniesRepository productionCompaniesRepository;

    @GetMapping("/")
    public String doInit() {
        List<ProductionCompanies>
        return "inicio";
    }
}
