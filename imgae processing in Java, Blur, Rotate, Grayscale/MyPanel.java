
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

public class MyPanel extends JPanel {

    int startX, flag, startY, endX, endY;
    BufferedImage grid;
    Graphics2D gc;

    public MyPanel() {
        startX = startY = 0;
        endX = endY = 100;
    }

    public MyPanel(int[] color) {
        startX = 0;
        startY = 0;
        endX = 150;
        endY = 300;
    }

    public void clear() {
        grid = null;
        repaint();
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        if (grid == null) {
            int w = this.getWidth();
            int h = this.getHeight();
            grid = (BufferedImage) (this.createImage(w, h));
            gc = grid.createGraphics();
        }
        g2.drawImage(grid, null, 0, 0);
    }

    public void drawHistogram() {
        for (int i = 0; i < 256; i++) {
            gc.drawLine(i, 0, i, 150);
        }
    }

    public void drawing() {
        gc.drawLine(startX, startY, endX, endY);
        repaint();
    }

}
