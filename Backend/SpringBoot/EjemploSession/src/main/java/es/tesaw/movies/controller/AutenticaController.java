package es.tesaw.movies.controller;

import es.tesaw.movies.dao.UserEditorRepository;
import es.tesaw.movies.entity.UserEditorEntity;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpSession;

@Controller
@AllArgsConstructor
public class AutenticaController {

    private final UserEditorRepository userEditorRepository;

    @GetMapping("/")
    public String doLogin () {
        return "login";
    }

    @PostMapping("/autentica")
    public String doAutentica (@RequestParam("username") String username,
                               @RequestParam("password") String password,
                               HttpSession session,
                               Model model) {
        UserEditorEntity editor = this.userEditorRepository.autheticate(username, password);
        if (editor == null) {
            model.addAttribute("error", "Usuario no encontrado o error de autenticación");
            return "login";
        } else {
            session.setAttribute("user", editor);
            return "redirect:/movies/";
        }
    }

    @GetMapping("/salir")
    public String doSalir (HttpSession session) {
        session.invalidate();
        return "redirect:/";
    }

}
