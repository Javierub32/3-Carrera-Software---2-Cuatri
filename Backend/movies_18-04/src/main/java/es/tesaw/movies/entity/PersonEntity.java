package es.tesaw.movies.entity;

import javax.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "PERSON")
@Getter
@Setter
@NoArgsConstructor
public class PersonEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String name;
    private Integer gender;

    @OneToMany(mappedBy = "person")
    private List<MovieCastEntity> castMovies = new ArrayList<>();

    @OneToMany(mappedBy = "person")
    private List<MovieCrewEntity> crewMovies = new ArrayList<>();
}
