/*
Daniel Robles Cantos 90%
IA 10%
*/
package com.leftjoiners.bancosol.proyectobackend.mapper;

import com.leftjoiners.bancosol.proyectobackend.dto.Distrito;
import com.leftjoiners.bancosol.proyectobackend.entity.DistritoEntity;
import org.springframework.stereotype.Component;
import java.util.stream.Collectors;

@Component
public class DistritoMapper extends MapperDTO<Distrito, DistritoEntity> {

    @Override
    public Distrito toDTO(DistritoEntity entity) {
        if (entity == null) return null;

        Distrito dto = new Distrito();
        dto.setId(entity.getId());
        dto.setNumero(entity.getNumero());
        dto.setNombre(entity.getNombre());

        if (entity.getTiendas() != null) {
            dto.setTiendas(entity.getTiendas().stream()
                    .map(tienda -> tienda.getId())
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