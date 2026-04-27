package es.taw.movies.repository;

import es.taw.movies.entity.ProductionCompanies;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductionCompaniesRepository extends JpaRepository<ProductionCompanies, Integer> {
}
