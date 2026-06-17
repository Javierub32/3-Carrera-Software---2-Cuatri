package es.tesaw.movies.entity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "USER_EDITOR")
@Getter
@Setter
@NoArgsConstructor
public class UserEditorEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String name;
    private String username;
    private String password;

    @OneToMany(mappedBy = "userEditor")
    private List<MovieEntity> movies = new ArrayList<>();


}
