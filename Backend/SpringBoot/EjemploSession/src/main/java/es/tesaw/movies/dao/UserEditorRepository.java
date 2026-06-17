package es.tesaw.movies.dao;

import es.tesaw.movies.entity.UserEditorEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface UserEditorRepository extends JpaRepository<UserEditorEntity, Integer> {

    @Query("select u from UserEditorEntity u where u.username = :un and u.password = :pwd")
    public UserEditorEntity autheticate (@Param("un")String username, @Param("pwd") String password);

}
