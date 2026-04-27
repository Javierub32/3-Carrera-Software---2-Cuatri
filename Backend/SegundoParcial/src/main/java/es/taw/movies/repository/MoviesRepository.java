package es.taw.movies.repository;

import es.taw.movies.entity.Movies;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface MoviesRepository extends JpaRepository<Movies, Integer> {

    @Query("SELECT DISTINCT m FROM Movies m JOIN m.productionCompaniesList p WHERE p.id IN :idsProductoras ")
    public List<Movies> findByIdsProductoras(@Param("idsProductoras") List<Integer> idsProductoras);
}
