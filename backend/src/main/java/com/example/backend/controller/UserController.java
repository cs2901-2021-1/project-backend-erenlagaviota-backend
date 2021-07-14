package com.example.backend.controller;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

import com.example.backend.config.TemporalData;
import com.example.backend.exception.ResourceNotFoundException;
import com.example.backend.model.User;
import com.example.backend.repository.UserRepository;
import com.example.backend.security.CurrentUser;
import com.example.backend.security.UserPrincipal;
import lombok.RequiredArgsConstructor;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class UserController {

    @Autowired
    UserRepository userRepository;

    @GetMapping("/profile")
    @PreAuthorize("hasRole('USER')")
    public Map<String, Object> getCurrentUser(@CurrentUser UserPrincipal userPrincipal)
            throws IllegalArgumentException, IllegalAccessException {
        Map<String, Object> userMap = new HashMap<String, Object>();
        User user = userRepository.findByEmail(userPrincipal.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", userPrincipal.getEmail()));
        Field[] userFields = user.getClass().getDeclaredFields();
        for (Field field : userFields) {
            field.setAccessible(true);
            Object value = field.get(user);
            userMap.put(field.getName(), value);
        }
        userMap.put("imageUrl", TemporalData.imageUrl.get(user.getEmail()));
        return userMap;
    }
}
