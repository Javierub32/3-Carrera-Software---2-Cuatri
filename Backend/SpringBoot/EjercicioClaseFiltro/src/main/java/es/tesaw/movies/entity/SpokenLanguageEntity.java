package es.tesaw.movies.entity;

import javax.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "SPOKEN_LANGUAGE")
@Getter
@Setter
@NoArgsConstructor
public class SpokenLanguageEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(unique = true, nullable = false)
    private String iso;

    private String name;

    @OneToMany(mappedBy = "originalLanguage")
    private List<MovieEntity> originalLanguageMovies = new ArrayList<>();

    @ManyToMany(mappedBy = "spokenLanguages")
    private List<MovieEntity> movies = new ArrayList<>();
}
