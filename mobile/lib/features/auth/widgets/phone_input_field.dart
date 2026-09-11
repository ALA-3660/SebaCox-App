import 'package:flutter/material.dart';

/// Reusable Mobile Number Input Field with Bangladeshi prefix (+880).
class PhoneInputField extends StatelessWidget {
  final TextEditingController controller;
  final ValueChanged<String>? onChanged;
  final String? errorText;
  final bool enabled;

  const PhoneInputField({
    super.key,
    required this.controller,
    this.onChanged,
    this.errorText,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'মোবাইল নম্বর দিন',
          style: TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.w600,
            color: Color(0xFF0F172A),
          ),
        ),
        const SizedBox(height: 8),
        TextField(
          controller: controller,
          enabled: enabled,
          keyboardType: TextInputType.phone,
          onChanged: onChanged,
          decoration: InputDecoration(
            hintText: '017XXXXXXXX',
            errorText: errorText,
            prefixIcon: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12),
              alignment: Alignment.center,
              width: 76,
              child: const Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    '+88',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 15,
                      color: Color(0xFF0F766E),
                    ),
                  ),
                  SizedBox(width: 6),
                  VerticalDivider(
                    width: 1,
                    thickness: 1,
                    color: Color(0xFFCBD5E1),
                  ),
                ],
              ),
            ),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10),
              borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10),
              borderSide: const BorderSide(color: Color(0xFF0F766E), width: 2),
            ),
            filled: true,
            fillColor: Colors.white,
          ),
        ),
      ],
    );
  }
}
