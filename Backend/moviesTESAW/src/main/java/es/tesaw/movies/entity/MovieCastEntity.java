package es.tesaw.movies.entity;

import javax.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "MOVIE_CAST")
@Getter
@Setter
@NoArgsConstructor
public class MovieCastEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "movie_id")
    private MovieEntity movie;

    @ManyToOne
    @JoinColumn(name = "person_id")
    private PersonEntity person;

    private String characterName;
    private Integer castOrder;
}
