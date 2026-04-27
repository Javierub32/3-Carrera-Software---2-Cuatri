package es.taw.movies.controller;

import es.taw.movies.entity.*;
import es.taw.movies.repository.MoviesRepository;
import es.taw.movies.repository.ProductionCompaniesRepository;
import es.taw.movies.repository.SpokenLanguagesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Controller
public class MoviesController {
    @Autowired
    private ProductionCompaniesRepository productionCompaniesRepository;

    @Autowired
    private MoviesRepository movieRepository;

    @Autowired
    private SpokenLanguagesRepository spokenLanguagesRepository;

    @GetMapping("/")
    public String doInit(Model model) {
        List<ProductionCompanies> productionCompanies = this.productionCompaniesRepository.findAll();
        List<Movies> movies = this.movieRepository.findAll();
        model.addAttribute("productionCompanies", productionCompanies);
        model.addAttribute("movies", movies);
        return "inicio";
    }

    @PostMapping("/filtrarPeliculas")
    public String filtrar(@RequestParam(value = "productoras", required = false) List<Integer> idsProductoras, Model model) {
        List<ProductionCompanies> productionCompanies = this.productionCompaniesRepository.findAll();
        List<Movies> movies = null;

        if (idsProductoras == null || idsProductoras.isEmpty()) {
            movies = this.movieRepository.findAll();
        } else {
            movies = this.movieRepository.findByIdsProductoras(idsProductoras);
        }

        model.addAttribute("productionCompanies", productionCompanies);
        model.addAttribute("movies", movies);
        model.addAttribute("idsProductoras", idsProductoras);
        return "inicio";
    }

    @GetMapping("/editarPelicula")
    public String editarPelicula(@RequestParam("id") Integer id, @RequestParam(value = "filtro", required = false) String filtro,Model model) {
        Movies movie = this.movieRepository.findById(id).get();
        List<SpokenLanguages> languages = this.spokenLanguagesRepository.findAll();
        List<SpokenLanguages> movieLanguages = movie.getSpokenLanguagesList();

        List<MovieCrew> peopleCrew;
        List<MovieCast> peopleCast;
        if (filtro != null) {
            if (filtro.equals("reparto")) {
                peopleCast = movie.getMovieCastList();
                peopleCrew = new ArrayList<>();
            } else {
                peopleCrew = movie.getMovieCrewList();
                peopleCast = new ArrayList<>();
            }
        } else {
            peopleCrew = new ArrayList<>();
            peopleCast = new ArrayList<>();
        }

        model.addAttribute("movie", movie);
        model.addAttribute("languages", languages);
        model.addAttribute("movieLanguages", movieLanguages);
        model.addAttribute("peopleCrew", peopleCrew);
        model.addAttribute("peopleCast", peopleCast);

        return "editarPelicula";
    }

    @PostMapping("/guardarPelicula")
    public String guardarPelicula(@RequestParam("id") Integer id,
                                  @RequestParam("title") String titulo,
                                  @RequestParam("fecha") @DateTimeFormat(pattern = "yyyy-MM-dd") Date fecha,
                                  @RequestParam("presupuesto") BigInteger presupuesto,
                                  @RequestParam(value = "languages", required = false) List<String> idiomas,
                                  @RequestParam("sinopsis") String sinopsis) {
        Movies movie = this.movieRepository.findById(id).get();

        List<SpokenLanguages> languages;
        if (idiomas == null || idiomas.isEmpty()) {
            languages = new ArrayList<>();
        } else {
            languages = this.spokenLanguagesRepository.findAllById(idiomas);
        }
        movie.setTitle(titulo);
        movie.setReleaseDate(fecha);
        movie.setBudget(presupuesto);
        movie.setSpokenLanguagesList(languages);
        movie.setOverview(sinopsis);
        this.movieRepository.save(movie);

        return "redirect:/";

    }


}
