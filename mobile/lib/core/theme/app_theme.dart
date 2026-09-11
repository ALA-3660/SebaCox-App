import 'package:flutter/material.dart';
import '../constants/app_colors.dart';
import 'app_typography.dart';

/// Application theme for SebaCox Mobile App.
/// Strictly enforces the GLOBAL BANGLA TYPOGRAPHY STANDARD:
/// - Large Heading: Hind Siliguri
/// - Medium Heading: Baloo Da 2
/// - Body & Normal Text: Tiro Bangla
class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      fontFamily: AppTypography.fontTiroBangla, // Default body font
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        primary: AppColors.primary,
        secondary: AppColors.primaryLight,
        background: AppColors.background,
        surface: AppColors.surface,
        error: AppColors.error,
      ),
      scaffoldBackgroundColor: AppColors.background,
      
      // Centralized TextTheme mapping to the three fonts
      textTheme: const TextTheme(
        // Large Headings (Hind Siliguri)
        displayLarge: AppTypography.largeHeading1,
        displayMedium: AppTypography.largeHeading2,
        headlineLarge: AppTypography.largeHeading2,
        headlineMedium: AppTypography.largeHeading3,
        
        // Medium Headings (Baloo Da 2)
        titleLarge: AppTypography.mediumHeading1,
        titleMedium: AppTypography.mediumHeading2,
        titleSmall: AppTypography.mediumHeading3,

        // Body Text & Normal Content (Tiro Bangla)
        bodyLarge: AppTypography.bodyLarge,
        bodyMedium: AppTypography.bodyMedium,
        bodySmall: AppTypography.bodySmall,
        labelLarge: AppTypography.label,
        labelMedium: AppTypography.listItem,
        labelSmall: AppTypography.helperText,
      ),

      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.surface,
        foregroundColor: AppColors.textPrimary,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: AppTypography.appBarTitle,
      ),

      cardTheme: CardTheme(
        color: AppColors.surface,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: AppColors.border, width: 1),
        ),
      ),

      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          minimumSize: const Size.fromHeight(50),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: AppTypography.buttonText,
        ),
      ),

      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        labelStyle: AppTypography.label,
        hintStyle: AppTypography.helperText,
        errorStyle: AppTypography.errorMessage,
        helperStyle: AppTypography.helperText,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: AppColors.border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: AppColors.border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: AppColors.primary, width: 2),
        ),
      ),
    );
  }
}

