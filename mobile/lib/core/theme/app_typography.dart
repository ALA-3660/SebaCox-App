import 'package:flutter/material.dart';
import '../constants/app_colors.dart';

/// ==================================================
/// GLOBAL BANGLA TYPOGRAPHY STANDARD FOR SEBACOX
/// ==================================================
/// 
/// FONT HIERARCHY:
/// 1. Large Heading -> Hind Siliguri
/// 2. Medium Heading -> Baloo Da 2
/// 3. Body / Normal Text -> Tiro Bangla
class AppTypography {
  // Primary Bangla Font Families
  static const String fontHindSiliguri = 'Hind Siliguri';
  static const String fontBalooDa2 = 'Baloo Da 2';
  static const String fontTiroBangla = 'Tiro Bangla';

  // --------------------------------------------------
  // 1. HIND SILIGURI: Large Headings & Main Page Titles
  // --------------------------------------------------
  
  /// Display Large / Hero Page Title (28sp, Bold)
  static const TextStyle largeHeading1 = TextStyle(
    fontFamily: fontHindSiliguri,
    fontSize: 28,
    fontWeight: FontWeight.w700,
    color: AppColors.textPrimary,
    letterSpacing: -0.5,
    height: 1.25,
  );

  /// Primary Section Heading / Screen Title (24sp, Bold)
  static const TextStyle largeHeading2 = TextStyle(
    fontFamily: fontHindSiliguri,
    fontSize: 24,
    fontWeight: FontWeight.w700,
    color: AppColors.textPrimary,
    letterSpacing: -0.3,
    height: 1.28,
  );

  /// Important Large Title / Modal Title (20sp, Bold)
  static const TextStyle largeHeading3 = TextStyle(
    fontFamily: fontHindSiliguri,
    fontSize: 20,
    fontWeight: FontWeight.w700,
    color: AppColors.textPrimary,
    height: 1.3,
  );

  /// Brand App Bar Title (18sp, Bold)
  static const TextStyle appBarTitle = TextStyle(
    fontFamily: fontHindSiliguri,
    fontSize: 18,
    fontWeight: FontWeight.w700,
    color: AppColors.primary,
    height: 1.2,
  );

  // --------------------------------------------------
  // 2. BALOO DA 2: Medium Headings, Cards & Button Prompts
  // --------------------------------------------------

  /// Section Title (18sp, Bold)
  static const TextStyle mediumHeading1 = TextStyle(
    fontFamily: fontBalooDa2,
    fontSize: 18,
    fontWeight: FontWeight.w700,
    color: AppColors.textPrimary,
    height: 1.35,
  );

  /// Card Heading / Sub-heading (16sp, SemiBold)
  static const TextStyle mediumHeading2 = TextStyle(
    fontFamily: fontBalooDa2,
    fontSize: 16,
    fontWeight: FontWeight.w600,
    color: AppColors.textPrimary,
    height: 1.35,
  );

  /// Sub-heading / Group Header (14sp, SemiBold)
  static const TextStyle mediumHeading3 = TextStyle(
    fontFamily: fontBalooDa2,
    fontSize: 14,
    fontWeight: FontWeight.w600,
    color: AppColors.textSecondary,
    height: 1.35,
  );

  /// Button Heading Text (15sp, Bold)
  static const TextStyle buttonText = TextStyle(
    fontFamily: fontBalooDa2,
    fontSize: 15,
    fontWeight: FontWeight.w700,
    color: Colors.white,
    letterSpacing: 0.3,
    height: 1.2,
  );

  /// Chip / Tab Text (13sp, SemiBold)
  static const TextStyle chipText = TextStyle(
    fontFamily: fontBalooDa2,
    fontSize: 13,
    fontWeight: FontWeight.w600,
    height: 1.2,
  );

  // --------------------------------------------------
  // 3. TIRO BANGLA: Body Text, Descriptions, Labels & Messages
  // --------------------------------------------------

  /// Large Body Text / Lead Description (15sp, Regular)
  static const TextStyle bodyLarge = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 15,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
    height: 1.6,
  );

  /// Standard Body Text (14sp, Regular)
  static const TextStyle bodyMedium = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 14,
    fontWeight: FontWeight.w400,
    color: AppColors.textSecondary,
    height: 1.6,
  );

  /// Small Body / Caption (12sp, Regular)
  static const TextStyle bodySmall = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 12,
    fontWeight: FontWeight.w400,
    color: AppColors.textSecondary,
    height: 1.5,
  );

  /// Field Label (13sp, Medium)
  static const TextStyle label = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 13,
    fontWeight: FontWeight.w500,
    color: AppColors.textPrimary,
    height: 1.4,
  );

  /// Helper Text / Footnote (11sp, Regular)
  static const TextStyle helperText = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 11,
    fontWeight: FontWeight.w400,
    color: AppColors.textSecondary,
    height: 1.4,
  );

  /// Form Input Text (14sp, Regular)
  static const TextStyle formText = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 14,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
  );

  /// Error Message Text (12sp, Regular)
  static const TextStyle errorMessage = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 12,
    fontWeight: FontWeight.w400,
    color: AppColors.error,
    height: 1.4,
  );

  /// Success Message Text (12sp, Regular)
  static const TextStyle successMessage = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 12,
    fontWeight: FontWeight.w400,
    color: AppColors.success,
    height: 1.4,
  );

  /// List Item Regular Text (13sp, Regular)
  static const TextStyle listItem = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 13,
    fontWeight: FontWeight.w400,
    color: AppColors.textPrimary,
    height: 1.5,
  );

  /// Motto / Quote Text (13sp, Italicized)
  static const TextStyle motto = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 13,
    fontStyle: FontStyle.italic,
    color: AppColors.textSecondary,
    height: 1.5,
  );
}
