/*
Daniel Robles Cantos: 100%
*/
package com.leftjoiners.bancosol.proyectobackend.service;

import com.leftjoiners.bancosol.proyectobackend.dao.DistritoRepository;
import com.leftjoiners.bancosol.proyectobackend.dto.Distrito;
import com.leftjoiners.bancosol.proyectobackend.entity.DistritoEntity;
import com.leftjoiners.bancosol.proyectobackend.mapper.DistritoMapper;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@AllArgsConstructor
public class DistritoService {
    private final DistritoRepository distritoRepository;
    private final DistritoMapper distritoMapper;

    public List<Distrito> listarDistritos() {
        List<DistritoEntity> distritos = this.distritoRepository.findAll();
        return this.distritoMapper.toDTOList(distritos);
    }
}