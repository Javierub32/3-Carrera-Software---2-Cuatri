/*
Daniel Robles Cantos: 100%
*/
package com.leftjoiners.bancosol.proyectobackend.service;

import com.leftjoiners.bancosol.proyectobackend.dao.MunicipioRepository;
import com.leftjoiners.bancosol.proyectobackend.dto.Municipio;
import com.leftjoiners.bancosol.proyectobackend.entity.MunicipioEntity;
import com.leftjoiners.bancosol.proyectobackend.mapper.MunicipioMapper;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@AllArgsConstructor
public class MunicipioService {
    private final MunicipioRepository municipioRepository;
    private final MunicipioMapper municipioMapper;

    public List<Municipio> listarMunicipios() {
        List<MunicipioEntity> municipios = this.municipioRepository.findAll();
        return this.municipioMapper.toDTOList(municipios);
    }
}