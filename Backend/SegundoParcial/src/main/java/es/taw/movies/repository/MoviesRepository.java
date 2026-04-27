package es.taw.movies.repository;

import es.taw.movies.entity.Movies;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MoviesRepository extends JpaRepository<Movies, Integer> {
}
