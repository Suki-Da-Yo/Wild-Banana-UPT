package com.msb.memesoundbar;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.Gravity;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class MainActivity extends Activity {
    private static final int BG = Color.rgb(12, 13, 18);
    private static final int CARD = Color.rgb(23, 25, 34);
    private static final int BORDER = Color.rgb(44, 48, 64);
    private static final int ACCENT = Color.rgb(158, 140, 255);
    private static final int TEXT = Color.rgb(245, 244, 250);
    private static final int MUTED = Color.rgb(169, 168, 179);

    private final List<Sound> sounds = new ArrayList<>();
    private LinearLayout list;
    private MediaPlayer player;
    private TextView activeCard;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        seedSounds();
        buildUi();
    }

    private void buildUi() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(16), dp(18), dp(16), dp(12));
        root.setBackgroundColor(BG);

        TextView title = text("Meme SoundBar", 30, TEXT, true);
        root.addView(title);
        TextView sub = text("MSB · Dota 2", 14, MUTED, false);
        root.addView(sub, margin(0, 2, 0, 14));

        EditText search = new EditText(this);
        search.setHint("Поиск по фразам, авторам и годам");
        search.setHintTextColor(MUTED);
        search.setTextColor(TEXT);
        search.setSingleLine(true);
        search.setPadding(dp(14), 0, dp(14), 0);
        search.setBackground(round(CARD, BORDER, 1));
        root.addView(search, new LinearLayout.LayoutParams(-1, dp(52)));

        TextView section = text("Реплики", 20, TEXT, true);
        root.addView(section, margin(0, 18, 0, 8));

        ScrollView scroll = new ScrollView(this);
        list = new LinearLayout(this);
        list.setOrientation(LinearLayout.VERTICAL);
        scroll.addView(list);
        root.addView(scroll, new LinearLayout.LayoutParams(-1, 0, 1f));
        setContentView(root);

        render("");
        search.addTextChangedListener(new TextWatcher() {
            public void beforeTextChanged(CharSequence s, int st, int c, int a) {}
            public void onTextChanged(CharSequence s, int st, int b, int c) { render(s.toString()); }
            public void afterTextChanged(Editable e) {}
        });
    }

    private void render(String query) {
        list.removeAllViews();
        String q = normalize(query);
        int shown = 0;
        for (Sound sound : sounds) {
            if (!q.isEmpty() && !sound.searchable().contains(q)) continue;
            TextView card = text(sound.title + "\n" + sound.source, 17, TEXT, true);
            card.setGravity(Gravity.CENTER_VERTICAL);
            card.setPadding(dp(16), dp(12), dp(16), dp(12));
            card.setMinHeight(dp(72));
            card.setBackground(round(CARD, BORDER, 1));
            card.setOnClickListener(v -> play(sound, card));
            list.addView(card, margin(0, 0, 0, 10));
            shown++;
        }
        if (shown == 0) {
            TextView empty = text("Ничего не найдено", 16, MUTED, false);
            empty.setGravity(Gravity.CENTER);
            list.addView(empty, margin(0, 30, 0, 0));
        }
    }

    private void play(Sound sound, TextView card) {
        stopPlayback();
        activeCard = card;
        card.setBackground(round(CARD, ACCENT, 3));
        player = new MediaPlayer();
        try {
            var afd = getAssets().openFd("audio/" + sound.file);
            player.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
            afd.close();
            player.setOnCompletionListener(mp -> stopPlayback());
            player.setOnErrorListener((mp, what, extra) -> {
                stopPlayback();
                Toast.makeText(this, "Не удалось воспроизвести звук", Toast.LENGTH_SHORT).show();
                return true;
            });
            player.prepare();
            player.start();
        } catch (IOException | RuntimeException e) {
            stopPlayback();
            Toast.makeText(this, "Аудиофайл не найден", Toast.LENGTH_SHORT).show();
        }
    }

    private void stopPlayback() {
        if (player != null) {
            try { player.stop(); } catch (Exception ignored) {}
            player.release();
            player = null;
        }
        if (activeCard != null) {
            activeCard.setBackground(round(CARD, BORDER, 1));
            activeCard = null;
        }
    }

    @Override protected void onStop() { super.onStop(); stopPlayback(); }
    @Override protected void onDestroy() { stopPlayback(); super.onDestroy(); }

    private void seedSounds() {
        add("Опаа, это что за пассажир?", "Team Spirit · 2023", "team_spirit_2023_passenger.mp3");
        add("Тише, мальчик", "Team Spirit · 2023", "team_spirit_2023_quiet_boy.mp3");
        add("Тяжелая жизнь саппорта", "Team Spirit · 2023", "team_spirit_2023_support_life.mp3");
        add("Старый Бог", "Team Spirit · 2024", "team_spirit_2024_old_god.mp3");
        add("Пушка бомба щас будет всё", "Team Spirit · 2024", "team_spirit_2024_bomb.mp3");
        add("Ты необучаем", "Team Spirit · 2024", "team_spirit_2024_unteachable.mp3");
        add("Ещё подвигаемся, пацаны", "Team Spirit · 2025", "team_spirit_2025_move.mp3");
        add("Забавы нету — ни ха-ха, ни хо-хо", "Team Spirit · 2025", "team_spirit_2025_no_fun.mp3");
        add("Я качаюсь слишком жёстко, мои мускулы слишком большие", "Team Spirit · 2025", "team_spirit_2025_muscles.mp3");
        add("Фри игра вообще, кто затроллит?", "Team Spirit · 2026", "team_spirit_2026_free_game.mp3");
        add("Помогите!", "Team Spirit · 2026", "team_spirit_2026_help.mp3");
        add("Короля не убить", "Team Spirit · 2026", "team_spirit_2026_king.mp3");
        add("М… Плаки-плаки?", "Vasilisa · 2024", "vasilisa_2024_plaki.mp3");
        add("А-а-а, это просто катастрофа!", "Vasilisa · 2024", "vasilisa_2024_catastrophe.mp3");
        add("О, какое же это мясо", "Vasilisa · 2025", "vasilisa_2025_meat.mp3");
        add("Киси-киси, мяу-мяу. Киси-киси, мя-мя-мяу", "Vasilisa · 2025", "vasilisa_2025_kisi.mp3");
        add("Охаёшечки-даттебаёшечки! Поанимешимся?", "Vasilisa · 2026", "vasilisa_2026_anime.mp3");
        add("Пёсик-пёсик. Ав-ав-ав!", "Vasilisa · 2026", "vasilisa_2026_dog.mp3");
    }

    private void add(String title, String source, String file) { sounds.add(new Sound(title, source, file)); }
    private String normalize(String s) { return s.toLowerCase(Locale.ROOT).replace('ё', 'е').trim(); }
    private TextView text(String s, int sp, int color, boolean bold) {
        TextView v = new TextView(this); v.setText(s); v.setTextSize(sp); v.setTextColor(color);
        if (bold) v.setTypeface(Typeface.DEFAULT, Typeface.BOLD); return v;
    }
    private GradientDrawable round(int fill, int stroke, int width) {
        GradientDrawable d = new GradientDrawable(); d.setColor(fill); d.setCornerRadius(dp(16)); d.setStroke(dp(width), stroke); return d;
    }
    private LinearLayout.LayoutParams margin(int l, int t, int r, int b) {
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(-1, -2); p.setMargins(dp(l), dp(t), dp(r), dp(b)); return p;
    }
    private int dp(int v) { return Math.round(v * getResources().getDisplayMetrics().density); }

    private final class Sound {
        final String title, source, file;
        Sound(String title, String source, String file) { this.title = title; this.source = source; this.file = file; }
        String searchable() { return normalize(title + " " + source); }
    }
}
