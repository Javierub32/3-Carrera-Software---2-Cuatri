/*
Daniel Robles Cantos 100%
*/
package com.leftjoiners.bancosol.proyectobackend.mapper;

import com.leftjoiners.bancosol.proyectobackend.dto.Zona;
import com.leftjoiners.bancosol.proyectobackend.entity.ZonaEntity;
import org.springframework.stereotype.Component;
import java.util.stream.Collectors;

@Component
public class ZonaMapper extends MapperDTO<Zona, ZonaEntity> {

    @Override
    public Zona toDTO(ZonaEntity entity) {
        if (entity == null) return null;

        Zona dto = new Zona();
        dto.setId(entity.getId());
        dto.setNombre(entity.getNombre());

        if (entity.getMunicipios() != null) {
            dto.setMunicipios(entity.getMunicipios().stream()
                    .map(municipio -> municipio.getId())
                    .collect(Collectors.toList()));
        }

        if (entity.getUsuarios() != null) {
            dto.setUsuarios(entity.getUsuarios().stream()
                    .map(usuario -> usuario.getId())
                    .collect(Collectors.toList()));
        }

        return dto;
    }
}