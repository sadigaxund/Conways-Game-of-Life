package pzemtsov;
import static util.LongUtil.hi;
import static util.LongUtil.lo;

class LongPoint1 extends LongPoint
{
    public static final LongPoint.Factory factory = new LongPoint.Factory ()
    {
        @Override
        public LongPoint1 create (long v)
        {
            return new LongPoint1 (v);
        }
    };

    private LongPoint1 (long v)
    {
        super (v);
    }

    @Override
    public int hashCode ()
    {
        return hi(v) * 3 + lo(v) * 5;
    }
}
