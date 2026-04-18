package es.tesaw.movies.dao;

import es.tesaw.movies.entity.MovieEntity;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface MoviesRepository extends JpaRepository<MovieEntity, Integer> {

    @Query("select m from MovieEntity m where m.originalTitle like concat('%', :cadena, '%') or m.overview like concat('%', :cadena, '%')")
    public List<MovieEntity> filtrarPorPalabra (@Param("cadena")String palabra);

    @Query("select distinct m from MovieEntity m join m.genres g where " +
            "g.id in (:generosId) and " +
            "(m.originalTitle like concat('%', :cadena, '%') or m.overview like concat('%', :cadena, '%'))")
    public List<MovieEntity> filtrarPorPalabraYGeneros (@Param("cadena")String palabra,
                                                        @Param("generosId")List<Integer> generosId);

    @Query("select distinct m from MovieEntity m join m.genres g where " +
            "g.id in (:generosId) and " +
            "(m.originalTitle like concat('%', :cadena, '%') or m.overview like concat('%', :cadena, '%'))")
    public List<MovieEntity> filtrarPorPalabraYGenerosYOrdenada (@Param("cadena")String palabra,
                                                        @Param("generosId")List<Integer> generosId,
                                                         Sort sort);
    @Query("select distinct m from MovieEntity m where " +
            "(m.originalTitle like concat('%', :cadena, '%') or m.overview like concat('%', :cadena, '%'))")
    public List<MovieEntity> filtrarPorPalabraYOrdenada (@Param("cadena")String palabra, Sort sort);

}
