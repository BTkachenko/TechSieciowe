import static java.lang.Thread.sleep;

public class Main {

    public static void main(String[] args) throws InterruptedException {
        CsmaSim simulation = new CsmaSim(10);

        simulation.addNode(0, 1,9);
        simulation.addNode(9 , 1,1);
        simulation.run();
    }


}