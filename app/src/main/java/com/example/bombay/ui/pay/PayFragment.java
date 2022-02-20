package com.example.bombay.ui.pay;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.bombay.databinding.FragmentPayBinding;
import com.example.bombay.ui.pay.PayViewModel;

public class PayFragment extends Fragment {

    private FragmentPayBinding binding;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        PayViewModel payViewModel =
                new ViewModelProvider(this).get(PayViewModel.class);

        binding = FragmentPayBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textPay;
        payViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}