/*
Daniel Robles Cantos 100%
*/
package com.leftjoiners.bancosol.proyectobackend.mapper;

import com.leftjoiners.bancosol.proyectobackend.dto.Municipio;
import com.leftjoiners.bancosol.proyectobackend.dto.Zona;
import com.leftjoiners.bancosol.proyectobackend.entity.MunicipioEntity;
import org.springframework.stereotype.Component;
import java.util.stream.Collectors;

@Component
public class MunicipioMapper extends MapperDTO<Municipio, MunicipioEntity> {

    @Override
    public Municipio toDTO(MunicipioEntity entity) {
        if (entity == null) return null;

        Municipio dto = new Municipio();
        dto.setId(entity.getId());
        dto.setNombre(entity.getNombre());

        if (entity.getZona() != null) {
            Zona z = new Zona();
            z.setId(entity.getZona().getId());
            z.setNombre(entity.getZona().getNombre());
            dto.setZona(z);
        }

        if (entity.getLocalidades() != null) {
            dto.setLocalidades(entity.getLocalidades().stream()
                    .map(localidad -> localidad.getId())
                    .collect(Collectors.toList()));
        }

        return dto;
    }
}