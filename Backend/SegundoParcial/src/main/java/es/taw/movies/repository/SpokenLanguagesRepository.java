package es.taw.movies.repository;

import es.taw.movies.entity.SpokenLanguages;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SpokenLanguagesRepository extends JpaRepository<SpokenLanguages, String> {
}
