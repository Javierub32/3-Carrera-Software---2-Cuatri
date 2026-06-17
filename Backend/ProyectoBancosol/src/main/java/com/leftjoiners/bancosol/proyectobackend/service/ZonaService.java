/*
Daniel Robles Cantos: 100%
*/
package com.leftjoiners.bancosol.proyectobackend.service;

import com.leftjoiners.bancosol.proyectobackend.dao.ZonaRepository;
import com.leftjoiners.bancosol.proyectobackend.dto.Zona;
import com.leftjoiners.bancosol.proyectobackend.entity.ZonaEntity;
import com.leftjoiners.bancosol.proyectobackend.mapper.ZonaMapper;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@AllArgsConstructor
public class ZonaService {
    private final ZonaRepository zonaRepository;
    private final ZonaMapper zonaMapper;

    public List<Zona> listarZonas() {
        List<ZonaEntity> zonas = this.zonaRepository.findAll();
        return this.zonaMapper.toDTOList(zonas);
    }
}