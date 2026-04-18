package es.tesaw.movies.controller;

import es.tesaw.movies.dao.GenreRepository;
import es.tesaw.movies.dao.MoviesRepository;
import es.tesaw.movies.dao.SpokenLanguageRepository;
import es.tesaw.movies.entity.GenreEntity;
import es.tesaw.movies.entity.MovieEntity;
import es.tesaw.movies.entity.SpokenLanguageEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.time.LocalDate;
import java.util.List;

@Controller
public class MoviesController {

    @Autowired
    protected MoviesRepository moviesRepository;

    @Autowired
    protected SpokenLanguageRepository spokenLanguageRepository;

    @Autowired
    protected GenreRepository genreRepository;

    @GetMapping("/")
    public String doInit (Model model) {

        List<MovieEntity> pelis = this.moviesRepository.findAll();
        List<GenreEntity> generos = this.genreRepository.findAll();
        model.addAttribute("pelis", pelis);
        model.addAttribute("generos", generos);
        return "movies";
    }

    @PostMapping("/filtrar")
    public String doFiltrar (@RequestParam(value = "filtro", required = false) String filtro,
                             @RequestParam(value = "generos", required = false) List<Integer> generosIds,
                             @RequestParam(value = "ordenarPor", required = false) String ordenarPor,
                             @RequestParam(value = "ascendente", required = false) Boolean ascendente,
                             Model model) {
        List<MovieEntity> lista;

        if (filtro.isEmpty() && generosIds == null && ordenarPor == null && ascendente == null) {
            lista = this.moviesRepository.findAll();
        } else if (generosIds == null && ordenarPor == null && ascendente == null) {
            lista = this.moviesRepository.filtrarPorPalabra(filtro);
        } else if (ordenarPor == null && ascendente == null) {
            lista = this.moviesRepository.filtrarPorPalabraYGeneros(filtro, generosIds);
        } else if (generosIds == null) {
            Sort sort;
            if (ascendente) {
                sort = Sort.by(Sort.Direction.ASC, ordenarPor);
            } else {
                sort = Sort.by(Sort.Direction.DESC, ordenarPor);
            }
            lista = this.moviesRepository.filtrarPorPalabraYOrdenada(filtro, sort);
        } else {
            Sort sort;
            if (ascendente) {
                sort = Sort.by(Sort.Direction.ASC, ordenarPor);
            } else {
                sort = Sort.by(Sort.Direction.DESC, ordenarPor);
            }
            lista = this.moviesRepository.filtrarPorPalabraYGenerosYOrdenada(filtro, generosIds, sort);
        }

        model.addAttribute("pelis", lista);
        return "movies_table";
    }

    protected String editarCrear (Integer id, Model model) {
        MovieEntity pelicula = null;
        if (id == null) {
            pelicula = new MovieEntity();
        } else {
            pelicula = this.moviesRepository.findById(id).get();
        }
        model.addAttribute("pelicula", pelicula);

        List<SpokenLanguageEntity> spokenLanguages = this.spokenLanguageRepository.findAll();
        model.addAttribute("idiomas", spokenLanguages);

        List<GenreEntity> genres = this.genreRepository.findAll();
        model.addAttribute("generos", genres);

        return "movie_edit";
    }

    @PostMapping("/anadir")
    public String doAnadir(Model model) {
      return this.editarCrear(null,model);
    }

    @GetMapping("/borrar")
    public String doBorrar(@RequestParam("id") Integer id) {
       MovieEntity pelicula = this.moviesRepository.findById(id).get();
       pelicula.deleteGeneres();
       pelicula.deleteProductionCompanies();
       pelicula.deleteSpokenLanguages();
       this.moviesRepository.delete(pelicula);
       return "redirect:/";
    }

    @GetMapping("/editar")
    public String doEditar (@RequestParam("id") Integer id, Model model) {
        return this.editarCrear(id,model);
    }

   @PostMapping("/guardar")
   public String doGuardar (@RequestParam(value = "id", required = false) Integer id,
                            @RequestParam(value = "titulo", required = false) String titulo,
                            @RequestParam(value = "sinopsis", required = false) String sinopsis,
                            @RequestParam(value = "titulo_orig", required = false)  String originalTitle,
                            @RequestParam(value = "fecha", required = false) @DateTimeFormat(pattern = "yyyy-MM-dd") LocalDate releaseDate,
                            @RequestParam(value = "runtime", required = false) Float runtime,
                            @RequestParam(value = "budget", required = false) Long budget,
                            @RequestParam(value = "revenue", required = false) Long revenue,
                            @RequestParam(value = "status", required = false) String status,
                            @RequestParam(value = "tagline", required = false) String tagline,
                            @RequestParam(value = "popularity", required = false) Float popularity,
                            @RequestParam(value = "voteAverage", required = false) Float voteAverage,
                            @RequestParam(value = "voteCount", required = false) Integer voteCount,
                            @RequestParam(value = "homepage", required = false) String homepage,
                            @RequestParam("idioma") Integer iddioma,
                            @RequestParam(value = "generos", required = false) List<Integer> generosIDs) {
        MovieEntity pelicula = null;
        if (id == null) {
            pelicula = new MovieEntity();
        } else {
            pelicula = this.moviesRepository.findById(id).get();
        }

        pelicula.setTitle(titulo);
        pelicula.setOriginalTitle(originalTitle);
        pelicula.setOverview(sinopsis);
        pelicula.setReleaseDate(releaseDate);
        pelicula.setRuntime(runtime);
        pelicula.setBudget(budget);
        pelicula.setRevenue(revenue);
        pelicula.setStatus(status);
        pelicula.setTagline(tagline);
        pelicula.setPopularity(popularity);
        pelicula.setVoteAverage(voteAverage);
        pelicula.setVoteCount(voteCount);
        pelicula.setHomepage(homepage);

        SpokenLanguageEntity idioma = this.spokenLanguageRepository.findById(iddioma).get();
        pelicula.setOriginalLanguage(idioma);

        if (generosIDs != null) {
            List<GenreEntity> genres = this.genreRepository.findAllById(generosIDs);
            pelicula.setGenres(genres);
        }

        this.moviesRepository.save(pelicula);
        return "redirect:/";
   }
}
