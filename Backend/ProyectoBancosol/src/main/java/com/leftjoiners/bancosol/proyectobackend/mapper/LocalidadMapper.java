/*
Daniel Robles Cantos 80%
IA 20%
*/
package com.leftjoiners.bancosol.proyectobackend.mapper;

import com.leftjoiners.bancosol.proyectobackend.dto.Localidad;
import com.leftjoiners.bancosol.proyectobackend.dto.Municipio;
import com.leftjoiners.bancosol.proyectobackend.dto.Zona;
import com.leftjoiners.bancosol.proyectobackend.entity.LocalidadEntity;
import org.springframework.stereotype.Component;
import java.util.stream.Collectors;

@Component
public class LocalidadMapper extends MapperDTO<Localidad, LocalidadEntity> {

    @Override
    public Localidad toDTO(LocalidadEntity entity) {
        if (entity == null) return null;

        Localidad dto = new Localidad();
        dto.setId(entity.getId());
        dto.setNombre(entity.getNombre());

        if (entity.getMunicipio() != null) {
            Municipio m = new Municipio();
            m.setId(entity.getMunicipio().getId());
            m.setNombre(entity.getMunicipio().getNombre());

            if (entity.getMunicipio().getZona() != null) {
                Zona z = new Zona();
                z.setId(entity.getMunicipio().getZona().getId());
                z.setNombre(entity.getMunicipio().getZona().getNombre());
                m.setZona(z);
            }
            dto.setMunicipio(m);
        }

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

        if (entity.getColaboradoresSede() != null) {
            dto.setColaboradoresSede(entity.getColaboradoresSede().stream()
                    .map(colaborador -> colaborador.getId())
                    .collect(Collectors.toList()));
        }

        if (entity.getColaboradoresColaboran() != null) {
            dto.setColaboradoresColaboran(entity.getColaboradoresColaboran().stream()
                    .map(colaborador -> colaborador.getId())
                    .collect(Collectors.toList()));
        }

        return dto;
    }
}