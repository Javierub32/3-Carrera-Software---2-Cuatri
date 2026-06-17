/*
Daniel Robles Cantos: 100%
*/
package com.leftjoiners.bancosol.proyectobackend.service;

import com.leftjoiners.bancosol.proyectobackend.dao.LocalidadRepository;
import com.leftjoiners.bancosol.proyectobackend.dto.Localidad;
import com.leftjoiners.bancosol.proyectobackend.entity.LocalidadEntity;
import com.leftjoiners.bancosol.proyectobackend.mapper.LocalidadMapper;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@AllArgsConstructor
public class LocalidadService {
    private final LocalidadRepository localidadRepository;
    private final LocalidadMapper localidadMapper;

    public List<Localidad> listarLocalidades() {
        List<LocalidadEntity> localidades = this.localidadRepository.findAll();
        return this.localidadMapper.toDTOList(localidades);
    }
}