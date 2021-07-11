package com.example.backend.security.oauth2.user;

import static com.example.backend.model.AuthProvider.GOOGLE;

import java.util.Map;

import com.example.backend.exception.OAuth2AuthenticationProcessingException;

public class OAuth2UserInfoFactory {
    public static OAuth2UserInfo getOAuth2UserInfo(String registrationId, Map<String, Object> attributes) {
        if (registrationId.equalsIgnoreCase(GOOGLE.toString())) {
            return new GoogleOAuth2UserInfo(attributes);
        } else {
            throw new OAuth2AuthenticationProcessingException("Login with this provider is not supported yet");
        }
    }
}
