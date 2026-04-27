package es.tesaw.movies.entity;

import javax.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "PRODUCTION_COMPANY")
@Getter
@Setter
@NoArgsConstructor
public class ProductionCompanyEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String name;

    @ManyToMany(mappedBy = "productionCompanies")
    private List<MovieEntity> movies = new ArrayList<>();
}
