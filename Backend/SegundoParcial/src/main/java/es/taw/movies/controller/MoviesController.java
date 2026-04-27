package es.taw.movies.controller;

import es.taw.movies.entity.Movies;
import es.taw.movies.entity.ProductionCompanies;
import es.taw.movies.repository.MoviesRepository;
import es.taw.movies.repository.ProductionCompaniesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class MoviesController {
    @Autowired
    private ProductionCompaniesRepository productionCompaniesRepository;

    @Autowired
    private MoviesRepository movieRepository;

    @GetMapping("/")
    public String doInit(Model model) {
        List<ProductionCompanies> productionCompanies = this.productionCompaniesRepository.findAll();
        List<Movies> movies = this.movieRepository.findAll();
        model.addAttribute("productionCompanies", productionCompanies);
        model.addAttribute("movies", movies);
        return "inicio";
    }
}
